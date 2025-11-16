const { getDriver } = require('./driver');
const { ct53 } = require('./CTs/CT53');

(async function main() {
  let driver = await getDriver();

  await ct53(driver)
  
})();