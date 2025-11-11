const { getDriver } = require('./driver');
const { ct51 } = require('./CTs/CT51');

(async function main() {
  let driver = await getDriver();

  await ct51(driver)
  
})();