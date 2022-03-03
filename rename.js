const fs = require("fs");
const path = require("path");

const folders = [
    path.join(__dirname, "cut_csv"),
    path.join(__dirname, "general_midi"),
    path.join(__dirname, "melodic_percussion_midi"),
    path.join(__dirname, "musescore_midi"),
    path.join(__dirname, "nbs")
];

folders.forEach((folder) => {
    if(!fs.existsSync(folder)) {
        console.log(`Folder ${folder} not found! Skipping...`);
        continue;
    }
    fs.readdirSync(folder).forEach((file) => {
        if(!fs.existsSync(path.join(folder, file))) {
            console.log(`File ${file} not found! Skipping...`);
            continue;
        }
        fs.renameSync(
            path.join(folder, file),
            path.join(folder, file.slice(4).replace(/_/gm, " "))
        );
    });
});