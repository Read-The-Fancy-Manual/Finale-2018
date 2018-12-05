<?php

putenv('NOT_FOR_YOU=zefrghaergjetùpogjaeùrgaerg');
$pdo = new PDO('sqlite:0950b8debd17539a1b46dfb2feab6006.sqlite');

$pdo->setAttribute(PDO::ATTR_DEFAULT_FETCH_MODE, PDO::FETCH_ASSOC);
$pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);

$pdo->query("CREATE TABLE IF NOT EXISTS torrents (filename STRING, magnet STRING)");
if ($pdo->query('SELECT count(*) FROM torrents')->fetch()['count(*)'] == 0) {
	$pdo->query("INSERT INTO torrents VALUES('FakeTacos.jpg', 'magnet:?xl=95250&dn=FakeTacos.jpg&xt=urn:tree:tiger:hb7zpzqvogoyeodnco5j75bawnhbm64t56637ia&ws=http://so.me.th.in.g/FakeTacos.jpg&xt=urn:ed2k:48bec9fab41623463dc88ea9878756d2&xt=urn:aich:73wrgc4pbdpxdgcypoa65j5feu5asevr'),('TacosFlag.jpg', 'magnet:?xl=16057&dn=TacosFlag.jpg&xt=urn:tree:tiger:y467u7hocx2257432ndrpdxioxfjocdycjwuicy&ws=http://so.me.th.in.g/TacosFlag9afde11aeb25ee6149875703765127e8.jpg&xt=urn:ed2k:f43622b3df2f5f6f8a316873f02bdd2c&xt=urn:aich:k4pzdts5sidkn3rz3auyydyp6y2duwdb'),('NachosButNotTacos.jpg','magnet:?xl=1638539&dn=NachosButNotTacos.jpg&xt=urn:tree:tiger:cnfzck54ybnapfpo7t6njl42rtps6nabl7rt6ky&ws=http://so.me.th.in.g/NachosButNotTacos.jpg&xt=urn:ed2k:35790b96b34f1af76ac3bf57ee25c941&xt=urn:aich:27vxcqa2xy2agjjda73pwsg3mtzcb7ox');");
}
