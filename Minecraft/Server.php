<?php

namespace Minecraft;

class Server
{
	protected $hostname;
	protected $port;

	public function __construct($hostname, $port = 25565)
	{
		if(stristr(':', $hostname))
		{
			list($hostname, $port) = explode(':', $hostname);
		}

		if($r = updateSrv($hostname))
		{
			list($hostname, $port) = $r;
		}

		$this->setHostname($hostname);
		$this->setPort($port);
	}

	public function setHostname($hostname)
	{
		$this->hostname = $hostname;
		return $this;
	}

	public function getHostname()
	{
		return $this->hostname;
	}

	public function setPort($port)
	{
		if(is_int($port))
		{
			$this->port = $port;
		}

		return $this;
	}

	public function getPort()
	{
		return $this->port;
	}

	// SRV 레코드 확인 후 업데이트
	public function updateSrv()
	{
		$dns = dns_get_record('_minecraft._tcp.' . $this->getHostname(), DNS_SRV);
		if(count($dns) > 0)
		{
			return [$dns[0]['target'], $dns[0]['port']];
		}

		return false;
	}
}