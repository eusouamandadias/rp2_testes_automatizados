const { getDriver } = require('./driver');
const { ct } = require('./CTs/CT49-2');

(async function main() {
  let driver = await getDriver();

  await ct(driver)
  
})();