<?php

namespace Minecraft;

class Status
{
	public static function retrieve(Server $server)
	{
		// 소켓 생성
		$socket = stream_socket_client(sprintf('tcp://%s:%u', $server->getHostname(), $server->getPort()), $errno, $errstr, 1);

		// 기본값 객체 생성
		$stats = new \stdClass();
		$stats->is_online = false;
		$stats->protocol_version = false;
		$stats->game_version = false;
		$stats->motd = false;
		$stats->online_players = false;
		$stats->max_players = false;

		// 접속이 되지 않을 경우
		if(!$socket)
		{
			return $stats;
		}

		// 필수 패킷 전송 후 소켓 종료
		fwrite($socket, "\xfe\x01");
    	$data = fread($socket, 1024); 
		fclose($socket);

		// 상태가 이상한 서버일 경우
		if($data == false && substr($data, 0, 1) != "\xFF")
		{
			return $stats;
		}

		// 수신한 패킷을 각 요소별로 분리
		$data = substr($data, 9);
		$data = mb_convert_encoding($data, 'auto', 'UCS-2');
		$data = explode("\x00", $data);

		// 객체에 값 대입
		$stats->is_online = true;
		list($stats->protocol_version, $stats->game_version, $stats->motd, $stats->online_players, $stats->max_players) = $data;

		return $stats;

	}

}