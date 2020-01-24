<?php
// Copyright 2020 Webstack. All rights reserved.
// 본 소프트웨어는 웹스택이 개발/운용하는 웹스택의 재산이나,
// 공공의 목적으로 개발되어 누구든지 자유롭게 소스코드를 활용할 수 있습니다.
// MIT 라이선스를 따르고 있으며, 라이선스와 관련된 자세한 정보는 동봉된 파일을 확인 바랍니다.
// 관련 문의는 해당되는 Github Repository 로 부탁드립니다.

foreach(array('Server', 'Status') as $file)
{
	require_once(sprintf('%s/Minecraft/%s.php', __DIR__, $file));
}

$stats = \Minecraft\Status::retreive(new \Minecraft\Server('ringfarm.kr'));
var_dump($stats);