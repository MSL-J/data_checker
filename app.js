const express = require("express");
const helmet = require("helmet");
const hpp = require("hpp");
const cors = require("cors");
const path = require("path");
const bodyParser = require("body-parser");
const { MONGODB } = require("./db/db");
const ObjectId = require("mongodb").ObjectID;

require("dotenv").config();
// const env = procees.env.NODE_ENV === 'PRODUCTION'
process.env.IS_DEV = process.env.NODE_ENV === "development" ? "1" : ""; // process.env 는 string화 되기 때문에 false가 'false' 가 되어서 굳이 '' 로 지정한다.
process.env.IS_PC =
  process.platform === "win32" || process.platform === "darwin" ? "1" : "";
process.env.PORT = process.env.PORT || "3030";
process.env.IS_PM2 =
  "PM2_HOME" in process.env ||
  "PM2_JSON_PROCESSING" in process.env ||
  "PM2_CLI" in process.env
    ? "true"
    : "";
process.env.HOST = require("os").hostname();
process.env.ROOT = __dirname;
console.log(
  `=== NODE_ENV : ${process.env.NODE_ENV}, PORT : ${process.env.PORT}, LOCAL : http://localhost:${process.env.PORT} ===`
);

const app = express();
app.use(bodyParser.json());

app.use(hpp());
app.use(helmet());
app.use(
  cors({
    origin: true,
    credentials: true,
  })
);

app.use(express.static(path.join(__dirname, "./dist")));

app.get("/api", (req, res, next) => {
  res.send("server connected");
});

// const Schema = mongoose.Schema;
// const HistorySchema = new Schema({}, { strict: false });
// const HistoryMdl = mongoose.model('history', HistorySchema, 'histories');

app.get("/piebarchart", async function (req, res, next) {
  console.log("piebar");
  const historyDoc = await MONGODB.collection("history")
    .find({})
    .sort({ _id: -1 })
    .limit(1)
    .toArray();
  res.json(historyDoc[0]);
});

app.get("/linechart", async function (req, res, next) {
  console.log("line");
  const historyDoc = await MONGODB.collection("history")
    .find({})
    .sort({ _id: -1 })
    .toArray();
  res.json(historyDoc);
});

app.get("/check", async function (req, res, next) {
  console.log("check");
  const historyDoc = await MONGODB.collection("history")
    .find({})
    .sort({ _id: -1 })
    .toArray();
  res.json(historyDoc);
});

app.post("/newcolor", async function (req, res, next) {
  const whichOne = async (which, i) => {
    if (which in data[i]) {
      console.log(which);

      await MONGODB.collection("mapping_table_color").updateOne(
        { _id: ObjectId(data[i].id) },
        { $set: { [which]: data[i][which] } }
      );
    }
  };
  console.log(req.body);
  const data = req.body;
  for (let i in data) {
    switch (Object.keys(data[i])[1]) {
      case "main_color":
        whichOne("main_color", i);
        break;
      case "color_kor":
        whichOne("color_kor", i);
        break;
      case "color_value":
        whichOne("color_value", i);
    }
  }
});

// app.post("/newcategory", async function (req, res, next) {
//   const whichOne = async (which, i) => {
//     if (which in data[i]) {
//       console.log(which);

//       await MONGODB.collection("mapping_table_category").create(
//         { _id: ObjectId(data[i].id) },
//         { $set: { [which]: data[i][which] } }
//       );
//     }
//   };
//   console.log(req.body);
//   const data = req.body;
//   for (let i in data) {
//     switch (Object.keys(data[i])[1]) {
//       case "shop_id":
//         whichOne("shop_id", i);
//         break;
//       case "original_category":
//         whichOne("original_category", i);
//         break;
//       case "balaan_category":
//         whichOne("balaan_category", i);
//     }
//   }
// });

app.post("/newmapping", function (req, res, next) {
  console.log(req.body);
  let spawn = require("child_process").spawn;
  let process = spawn("python", [
    "./python/newMap.py",
    //값이 객체 일때 스트링으로 변환해서 전달
    // JSON.stringify(req.body.first),
    //값이 스트링일때는 그대로
    req.body.save,
    req.body.mode,
  ]);

  process.stdout.on("data", (data) => {
    let textChunk = data.toString("utf8");
    console.log(textChunk);
    res.json(textChunk);
  });
});

app.get("/datatable/color", async function (req, res) {
  console.log("color");
  const result = await MONGODB.collection("mapping_table_color")
    .find({})
    .toArray();
  res.json(result);
});

app.get("/datatable/category", async function (req, res) {
  const result = await MONGODB.collection("metadata")
    .find({ cate: "category" })
    .toArray();
  res.json(result);
});

// app.get("/piechart", function (req, res, next) {
//   var spawn = require("child_process").spawn;
//   var process = spawn("python", ["./python/aaa.py"], { stdio: "pipe" });
//   process.stdout.on("data", (data) => {
//     console.log(data.toString());
//     res.send(data.toString());
//   });
//   process.stderr.on("data", (data) => {
//     console.error("err", data.toString());
//     // res.send(data.toString());
//   });
// });

// app.post("/testtest", function (req, res, next) {
//   console.log(req.body);
//   let spawn = require("child_process").spawn;
//   let process = spawn("python", [
//     "./python/test.py",
//     //값이 객체 일때 스트링으로 변환해서 전달
//     JSON.stringify(req.body.first),
//     //값이 스트링일때는 그대로
//     req.body.last,
//   ]);

//   process.stdout.on("data", (data) => {
//     console.log(data.toString());
//     res.send(data.toString());
//   });
// });

module.exports = app;
