// CREATE TABLE defense_research (
// id INT AUTO_INCREMENT PRIMARY KEY,
// country VARCHAR(50),
// title VARCHAR(255),
// category VARCHAR(100),
// research_year INT,
// commercialization_stage VARCHAR(50),
// summary TEXT
// );

// 위와 같은 내용을 mysql에 입력
// 정형 데이터 위주이며, 향후 TEXT, JSON 컬럼으로 비정형 데이터 확장 가능

import mysql from "mysql2/promise";


export const pool = mysql.createPool({
host: "localhost",
user: "root",
password: "password",
database: "defense",
});