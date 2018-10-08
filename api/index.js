"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
Object.defineProperty(exports, "__esModule", { value: true });
const Datastore = require('@google-cloud/datastore');
const datastore = Datastore();
exports.projectsGET = (res, req) => {
    return datastore.runQuery(datastore.createQuery('project')).then((results) => {
        return results[0];
    });
};
//# sourceMappingURL=index.js.map