#!/usr/bin/env python
"""
Copyright (c) 2006-2018 sqlmap developers (http://sqlmap.org/)
See the file 'LICENSE' for copying permission
"""
import re
from lib.core.common import randomRange
from lib.core.data import kb
from lib.core.enums import PRIORITY
__priority__ = PRIORITY.NORMAL
def dependencies():
    pass
def tamper(payload, **kwargs):
    """
    Replaces each SQLite keyword and core functions character with mixed case value (e.g. SELECT -> SeLeCt)
    
    Requirement:
        * SQLite
    Tested against:
        * SQLite 3
    Notes:
        * Useful to bypass very weak and bespoke web application firewalls
          that has poorly written permissive regular expressions
        * This tamper script should work against all (?) databases
        * Usefull when some keywords like 'as' are part or words like 'last'
          and that randomcase temper script get you caught because it outputted
          'lasT' ('as' is flagged where 'aS' or 'As' is not).
    """
    retVal = payload
    if payload:
        for match in re.finditer(r"\b[A-Za-z_]+\b", retVal):
            word = match.group()
            # Some words can't be filtered or fingerprinting and dump will fail
            # type='table' or FROM sqlite_master need to be untouched 
            # see https://www.sqlite.org/fileformat.html#storage_of_the_sql_database_schema
            whitelist = ['TABLE','SQLITE_MASTER','TYPE','NAME','TBL_NAME','ROOTPAGE','SQL']
            # SQLite keywords - see https://www.sqlite.org/lang_keywords.html
            keywords = ['ABORT','ACTION','ADD','AFTER','ALL','ALTER','ANALYZE','AND','AS','ASC','ATTACH','AUTOINCREMENT','BEFORE','BEGIN','BETWEEN','BY','CASCADE','CASE','CAST','CHECK','COLLATE','COLUMN','COMMIT','CONFLICT','CONSTRAINT','CREATE','CROSS','CURRENT','CURRENT_DATE','CURRENT_TIME','CURRENT_TIMESTAMP','DATABASE','DEFAULT','DEFERRABLE','DEFERRED','DELETE','DESC','DETACH','DISTINCT','DO','DROP','EACH','ELSE','END','ESCAPE','EXCEPT','EXCLUSIVE','EXISTS','EXPLAIN','FAIL','FILTER','FOLLOWING','FOR','FOREIGN','FROM','FULL','GLOB','GROUP','HAVING','IF','IGNORE','IMMEDIATE','IN','INDEX','INDEXED','INITIALLY','INNER','INSERT','INSTEAD','INTERSECT','INTO','IS','ISNULL','JOIN','KEY','LEFT','LIKE','LIMIT','MATCH','NATURAL','NO','NOT','NOTHING','NOTNULL','NULL','OF','OFFSET','ON','OR','ORDER','OUTER','OVER','PARTITION','PLAN','PRAGMA','PRECEDING','PRIMARY','QUERY','RAISE','RANGE','RECURSIVE','REFERENCES','REGEXP','REINDEX','RELEASE','RENAME','REPLACE','RESTRICT','RIGHT','ROLLBACK','ROW','ROWS','SAVEPOINT','SELECT','SET','TEMP','TEMPORARY','THEN','TO','TRANSACTION','TRIGGER','UNBOUNDED','UNION','UNIQUE','UPDATE','USING','VACUUM','VALUES','VIEW','VIRTUAL','WHEN','WHERE','WINDOW','WITH','WITHOUT']
            # Some SQLite core functions - see https://www.sqlite.org/lang_corefunc.html
            core_functions = ['ABS','CHANGES','CHAR','COALESCE','GLOB','HEX','IFNULL','INSTR','LAST_INSERT_ROWID','LENGTH','LIKE','LIKELIHOOD','LIKELY','LOAD_EXTENSION','LOWER','LTRIM','MAX','MIN','NULLIF','PRINTF','QUOTE','RANDOM','RANDOMBLOB','REPLACE','ROUND','RTRIM','SOUNDEX','SQLITE_COMPILEOPTION_GET','SQLITE_COMPILEOPTION_USED','SQLITE_OFFSET','SQLITE_SOURCE_ID','SQLITE_VERSION','SUBSTR','TOTAL_CHANGES','TRIM','TYPEOF','UNICODE','UNLIKELY','UPPER','ZEROBLOB']
            # common SQL reserved words - see https://www.drupal.org/docs/develop/coding-standards/list-of-sql-reserved-words
            common = ['ANY','COUNT']
            blacklist = list(set().union(keywords, core_functions, common))
            if word.upper() in kb.keywords or ("%s(" % word) in payload or word.upper() in blacklist:
                if word.upper() in whitelist:
                    break
                while True:
                    _ = ""
                    for i in xrange(len(word)):
                        _ += word[i].upper() if i%2==0 else word[i].lower()
                    if len(_) > 1 and _ not in (_.lower(), _.upper()):
                        break
                retVal = retVal.replace(word, _)
    return retVal
