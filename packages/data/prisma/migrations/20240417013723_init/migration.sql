-- CreateTable
CREATE TABLE "recorders" (
    "id" TEXT NOT NULL PRIMARY KEY,
    "location_id" TEXT NOT NULL,
    CONSTRAINT "recorders_location_id_fkey" FOREIGN KEY ("location_id") REFERENCES "locations" ("id") ON DELETE RESTRICT ON UPDATE CASCADE
);

-- CreateTable
CREATE TABLE "locations" (
    "id" TEXT NOT NULL PRIMARY KEY,
    "latitude" REAL NOT NULL,
    "longitude" REAL NOT NULL
);
