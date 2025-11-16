const { getDriver } = require('./driver');
const { ct55 } = require('./CTs/CT55');

(async function main() {
  let driver = await getDriver();

  await ct55(driver)
  
})();