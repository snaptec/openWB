import 'package:dartnissanconnect/dartnissanconnect.dart';
import 'package:args/args.dart';
import 'dart:io';

getBatteryStatus(NissanConnectVehicle vehicle) async {
   var battery = await vehicle.requestBatteryStatus();
   
   return battery.batteryPercentage;
}

sendRefreshRequest(NissanConnectVehicle vehicle) async {
  await Future.delayed(Duration(seconds: 1));
  await vehicle.requestBatteryStatusRefresh();
  await Future.delayed(Duration(seconds: 1));
}


updateSocStatus(NissanConnectVehicle vehicle, File myfile, bool verbose) async {
  var battery = await getBatteryStatus(vehicle);

  var sink = myfile.openWrite();
  sink.write(double.parse(battery.replaceAll('%', '')).round());
  sink.close();
  if (verbose) {
     print("Got Value: " + battery);
  }
}

updateSocFull(NissanConnectVehicle vehicle, File myfile, bool verbose) async {
    if (verbose) {
      print("Reading SOC...");
    }
    await updateSocStatus(vehicle,  myfile, verbose);

    if (verbose) {
      print("Request SOC update");
    }
    await sendRefreshRequest(vehicle);

    if (verbose) {
      print("Reading SOC again...");
    }
    await updateSocStatus(vehicle,  myfile, verbose);
}

main(List<String> args) {

  var parser = ArgParser();
  parser.addOption('username', abbr: 'u', mandatory: true, help: 'your nissanconnect user name');
  parser.addOption('password', abbr: 'p', mandatory: true, help: 'your nissanconnect password');
  parser.addOption('socfile', abbr: 'f', mandatory: true, help: 'the file to write soc to');
  parser.addFlag('verbose', abbr: 'v', defaultsTo: false, help: 'debug info');
  parser.addFlag('debug', abbr: 'd', defaultsTo: false, help: 'debug info');

  var results;

  try {
    results = parser.parse(args);
  } on ArgParserException {
    print(parser.usage);
    exit(0);
  }

  NissanConnectSession session = new NissanConnectSession(debug:  results['debug']);
  
  if (results['verbose']) {
    print("Logging in...");
  }
 
  session.login(username: results['username'], password: results['password']).then((vehicle) {

    var myfile = File( results['socfile']);

    updateSocFull(vehicle,  myfile, results['verbose']);

    });
}
