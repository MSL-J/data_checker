module.exports = {
  root: true,
  env: {
    node: true,
  },
  extends: [
    "plugin:vue/essential",
    // "plugin:node/recommended",
    "plugin:prettier/recommended",
    "eslint:recommended",
  ],
  rules: {
    "no-console": process.env.NODE_ENV === "production" ? "error" : "off",
    "no-debugger": process.env.NODE_ENV === "production" ? "error" : "off",
  },
  parserOptions: {
    sourceType: "module",
    parser: "babel-eslint",
    ecmaVersion: 2020,
    // allowImportExportEverywhere: true,
  },
};