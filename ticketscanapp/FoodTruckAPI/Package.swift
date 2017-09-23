import PackageDescription

let package = Package(
    name: "FoodTruckAPI",
    targets: [
      Target(
        name: "FoodTruckServer",
        dependencies: [ .Target(name: "FoodTruckAPI") ]
      ),
      Target(
        name: "FoodTruckAPI"
      )
    ],
    dependencies: [
      .Package(url: "https://github.com/IBM-Swift/Kitura.git", majorVersion: 1, minor: 6),
      .Package(url: "https://github.com/IBM-Swift/Kitura-CouchDB.git", majorVersion: 1, minor: 6),
      .Package(url: "https://github.com/IBM-Swift/Swift-cfenv", majorVersion: 2, minor: 0), 
    ]
)
