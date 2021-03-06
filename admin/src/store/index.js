import Vue from "vue";
import Vuex from "vuex";
import createLogger from "vuex/dist/logger";
import { Post, Tag, Account, Setting, Auth, Role, Permission } from "./modules";

Vue.use(Vuex);

const store = new Vuex.Store({
  plugins: process.env.NODE_ENV === "production" ? [] : [createLogger()],
  modules: {
    Account,
    Post,
    Tag,
    Setting,
    Auth,
    Role,
    Permission
  }
});

if (module.hot) {
  module.hot.accept(["./modules"], () => {
    const newMutations = require("./modules").default;

    store.hotUpdate({
      mutations: newMutations
    });
  });
}

export default store;
