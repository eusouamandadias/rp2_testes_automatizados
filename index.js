const { getDriver } = require('./driver');
const { ct54 } = require('./CTs/CT54');

(async function main() {
  let driver = await getDriver();

  await ct54(driver)
  
})();