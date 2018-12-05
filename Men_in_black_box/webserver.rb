require 'sinatra'
require 'sqlite3'

configure do
  set :public_folder, 'public'
  set :views, 'views'
  set :bind, '0.0.0.0'
  enable :sessions
  set :environment, :production
  #disable :protection
  set :session_secret, '8e619d29a7646692e6f3642c4ec29be892d8ed53a77a7271e02bcde6620b807be1eb26b76ca7cc83a39bc0f19dba5a281c29ce7a255d7b699be32df2e82b37c1'
end

def authenticate!
  unless session[:user]
    redirect to('/login')
  end
end

def sqlite_filter(str)
  # I removed some keywords from the blacklist as it was to difficult to solve, for example 'as' is in 'sqlite_master'
  # whitelist LIMIT,WHERE,FROM,DO,AND because of https://github.com/sqlmapproject/sqlmap/issues/3384
  # whitelist = ['AS','as','TABLE','table','LIMIT','FROM','WHERE','DO','AND']
  # SQLite keywords - see https://www.sqlite.org/lang_keywords.html
  keywords = ['ABORT','ACTION','ADD','AFTER','ALL','ALTER','ANALYZE','ASC','ATTACH','AUTOINCREMENT','BEFORE','BEGIN','BETWEEN','BY','CASCADE','CASE','CAST','CHECK','COLLATE','COLUMN','COMMIT','CONFLICT','CONSTRAINT','CREATE','CROSS','CURRENT','CURRENT_DATE','CURRENT_TIME','CURRENT_TIMESTAMP','DATABASE','DEFAULT','DEFERRABLE','DEFERRED','DELETE','DESC','DETACH','DISTINCT','DROP','EACH','ELSE','END','ESCAPE','EXCEPT','EXCLUSIVE','EXISTS','EXPLAIN','FAIL','FILTER','FOLLOWING','FOR','FOREIGN','FULL','GLOB','GROUP','HAVING','IF','IGNORE','IMMEDIATE','IN','INDEX','INDEXED','INITIALLY','INNER','INSERT','INSTEAD','INTERSECT','INTO','IS','ISNULL','JOIN','KEY','LEFT','LIKE','MATCH','NATURAL','NO','NOT','NOTHING','NOTNULL','NULL','OF','OFFSET','ON','OR','ORDER','OUTER','OVER','PARTITION','PLAN','PRAGMA','PRECEDING','PRIMARY','QUERY','RAISE','RANGE','RECURSIVE','REFERENCES','REGEXP','REINDEX','RELEASE','RENAME','REPLACE','RESTRICT','RIGHT','ROLLBACK','ROW','ROWS','SAVEPOINT','SELECT','SET','TEMP','TEMPORARY','THEN','TO','TRANSACTION','TRIGGER','UNBOUNDED','UNION','UNIQUE','UPDATE','USING','VACUUM','VALUES','VIEW','VIRTUAL','WHEN','WINDOW','WITH','WITHOUT','abort','action','add','after','all','alter','analyze','and','asc','attach','autoincrement','before','begin','between','by','cascade','case','cast','check','collate','column','commit','conflict','constraint','create','cross','current','current_date','current_time','current_timestamp','database','default','deferrable','deferred','delete','desc','detach','distinct','do','drop','each','else','end','escape','except','exclusive','exists','explain','fail','filter','following','for','foreign','from','full','glob','group','having','if','ignore','immediate','in','index','indexed','initially','inner','insert','instead','intersect','into','is','isnull','join','key','left','like','limit','match','natural','no','not','nothing','notnull','null','of','offset','on','or','order','outer','over','partition','plan','pragma','preceding','primary','query','raise','range','recursive','references','regexp','reindex','release','rename','replace','restrict','right','rollback','row','rows','savepoint','select','set','temp','temporary','then','to','transaction','trigger','unbounded','union','unique','update','using','vacuum','values','view','virtual','when','where','window','with','without']
  # SQLite core functions - see https://www.sqlite.org/lang_corefunc.html
  core_functions = ['ABS','CHANGES','CHAR','COALESCE','GLOB','HEX','IFNULL','INSTR','LAST_INSERT_ROWID','LENGTH','LIKE','LIKELIHOOD','LIKELY','LOAD_EXTENSION','LOWER','LTRIM','MAX','MIN','NULLIF','PRINTF','QUOTE','RANDOM','RANDOMBLOB','REPLACE','ROUND','RTRIM','SOUNDEX','SQLITE_COMPILEOPTION_GET','SQLITE_COMPILEOPTION_USED','SQLITE_OFFSET','SQLITE_SOURCE_ID','SQLITE_VERSION','SUBSTR','TOTAL_CHANGES','TRIM','TYPEOF','UNICODE','UNLIKELY','UPPER','ZEROBLOB','abs','changes','char','coalesce','glob','hex','ifnull','instr','last_insert_rowid','length','like','likelihood','likely','load_extension','lower','ltrim','max','min','nullif','printf','quote','random','randomblob','replace','round','rtrim','soundex','sqlite_compileoption_get','sqlite_compileoption_used','sqlite_offset','sqlite_source_id','sqlite_version','substr','total_changes','trim','typeof','unicode','unlikely','upper','zeroblob']
  # common SQL reserved words - see https://www.drupal.org/docs/develop/coding-standards/list-of-sql-reserved-words
  common = ['ANY','COUNT','any','count']

  blacklist = keywords | core_functions | common

  r=/#{blacklist.join('|')}/ # faster to convert the array of strings into a Regexp
  message = 'Naughty hacker'
  if str.match(r)
    redirect to("/login?message=#{message}") 
    return ''
  else
    return str
  end
end

get '/' do
  authenticate!
  redirect to('/home')
end

get '/login' do
  @message = params['message']
  erb :login
end

post '/auth' do
  # Open a database
  db = SQLite3::Database.new 'database.db', {readonly: true}
  filtered_user = sqlite_filter(params['user'])
  filtered_password = sqlite_filter(params['pass'])
  query = 'SELECT username, password FROM users WHERE username="' + filtered_user + '" AND password="' + filtered_password + '";'
  rows = db.execute(query)
  db.close
  unless rows.empty?
    username, password = rows.first
    session.clear
    session[:user] = filtered_user
    redirect to('/home')
  else
    sleep 0.1
    message = 'Wrong credentials!'
    redirect to("/login?message=#{message}") 
  end
end

get '/home' do
  authenticate!
  @user = session[:user]
  erb :home
end

get '/logout' do
  session.clear
  message = 'You have been signed out.'
  redirect to("/login?message=#{message}") 
end
