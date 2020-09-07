const mongoose = require("mongoose");
require("dotenv").config();

const location = process.env.MONGODB_LOCATION;
const MONGODB = mongoose.createConnection(location, {
  dbName: "balaan",
  useNewUrlParser: true,
  useUnifiedTopology: true,
  useFindAndModify: false,
  useCreateIndex: true,
});

module.exports = {
  MONGODB,
};
