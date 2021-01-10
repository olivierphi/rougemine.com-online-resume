import * as path from "path";
import { writeFile } from "fs/promises";

import * as React from "react";
import { renderToStaticMarkup } from "react-dom/server";
import * as prettier from "prettier";

import { Resume } from "../src/components/Resume";
import { LANG } from "../src/domain";

const VALID_LANGUAGES = ["en", "fr"];
const DOCTYPE = "<!DOCTYPE html>"; // this cannot be generated by React

const langCode: string = process.env["LANG_CODE"] ?? "en"; // we'd better not use "LANG", as the OS already sets it

if (!isValidLang(langCode)) {
  console.error(`"${langCode}" is not a valid language code (should be ${VALID_LANGUAGES.join("|")})`);
  process.exit(1);
}

const htmlCode = DOCTYPE + renderToStaticMarkup(<Resume lang={langCode} />);
// The original promise of the Web was to be able to read the source of an HTML page, let's keep
// that sprit alive ^_^ (even though Dev Tools can beautify if we ask them to of course)
const htmlCodeReadable = prettier.format(htmlCode, { parser: "html" });

const targetFilePath = path.join(__dirname, "../", "dist", `${langCode}.html`);

writeFile(targetFilePath, htmlCodeReadable, { encoding: "utf-8" })
  .then(() => {
    console.log(`HTML page generated in "${path.resolve(targetFilePath)}".`);
  })
  .catch((err) => {
    console.error(err);
    process.exit(1);
  });

function isValidLang(langCode: string): langCode is LANG {
  return VALID_LANGUAGES.includes(langCode);
}