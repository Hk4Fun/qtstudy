DROP TABLE IF EXISTS bill_list;
CREATE TABLE bill_list(
	createTime TEXT PRIMARY KEY DEFAULT (datetime('now','localtime')),
	orderID CHAR(50) NOT NULL,
	roomID CHAR(50) NOT NULL,
	userLevel TINYINT NOT NULL,
	cost FLOAT NOT NULL,
	discount FLOAT NOT NULL,
	receive FLOAT NOT NULL,
	CHECK (userLevel IN (0, 1))
	CHECK (discount <= 1 AND discount >= 0)
	CHECK (receive = cost * discount)
);

DROP TABLE IF EXISTS detail_list;
CREATE TABLE detail_list(
	roomID CHAR(50) NOT NULL,
	openTime INT NOT NULL,
	closeTime INT NOT NULL,
	userLevel TINYINT NOT NULL,
	tempAdjust INT NOT NULL DEFAULT 0,
	tempBackCount INT NOT NULL DEFAULT 0,
	speedAdjust INT NOT NULL DEFAULT 0,
	energy FLOAT NOT NULL DEFAULT 0,
	cost FLOAT NOT NULL,
	orderID CHAR(50) NOT NULL,
	CHECK (userLevel IN (0, 1))
	PRIMARY KEY (roomID, openTime)
)