import "./index.css";

import { createApp } from "vue";
import router from "./router";
import App from "./App.vue";

import { Button, setConfig, ntsRequest, resourcesPlugin } from "frappe-ui";

const app = createApp(App);

setConfig("resourceFetcher", ntsRequest);

app.use(router);
app.use(resourcesPlugin);

app.component("Button", Button);
app.mount("#app");
