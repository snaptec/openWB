<?php
class openWBSettings {

	private $configFile = "";
	private $settings = [];

	function __construct($file = '../../openwb.conf') {
		if ( file_exists($file) ) {
			$this->configFile = $file;
			$this->readConfigFile();
		} else {
			die("Konfigurationsdatei nicht gefunden: $file" );
			// hier eventuell eine Standardkonfiguration erstellen?
		}
	}

	private function readConfigFile() {
		// first read config-lines in array
		$settingsFile = file($this->configFile);

		// convert lines to key/value array for faster manipulation
		foreach($settingsFile as $line) {
			// check for comment-lines in older config files and don't process them
			if ( strlen(trim($line)) > 3 && $line[0] != "#" ) {
				// split line at char '='
				$splitLine = explode('=', $line, 2);
				// trim parts
				$splitLine[0] = trim($splitLine[0]);
				$splitLine[1] = trim($splitLine[1]);
				// push key/value pair to new array
				$this->settings[$splitLine[0]] = $splitLine[1];
			}
		}
	}

	public function saveConfigFile() {
		// write config to file
		$fp = fopen($this->configFile, "w");
		if ( $fp ) {
			foreach($this->settings as $key => $value) {
				fwrite($fp, $key.'='.$value."\n");
			}
		} else {
			die("Konfigurationsdatei konnte nicht geschrieben werden: $this->configFile");
		}
	}

	public function dumpSettings() {
		return print_r($this->settings, true);
	}

	public function getSetting($getKey) {
		if(array_key_exists($getKey, $this->settings)) {
			return $this->settings[$getKey];
		}
		return null;
	}

	public function addSetting($addKey, $addValue) {
		if(!array_key_exists($setKey, $this->settings)) {
			$this->settings[$setKey] = $value;
		} else {
			$this->setSettings($addKey, $addValue);
		}
	}

	public function setSettings($newSettings = []) {
		foreach($newSettings as $newKey => $newValue){
			$this->setSetting($newKey, $newValue);
		}
	}

	private function setSetting($setKey, $value = '') {
		if(array_key_exists($setKey, $this->settings)) {
			$this->settings[$setKey] = $value;
		}
	}
}
?>
