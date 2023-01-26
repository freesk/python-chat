<template>
  <div class="container mx-auto">
    <div class="mt-8">
      <h1 class="text-5xl">Python Chat</h1>
      <p v-if="username" class="mt-2">Hello {{ username }}</p>
      <a
        v-if="username"
        href="#"
        class="text-blue-600 dark:text-blue-500 hover:underline"
        @click="logout"
        >Logout</a
      >
    </div>

    <div class="bg-gray-200 rounded-xl shadow border p-8 m-10">
      <Chat v-if="username" />
      <UsernamePrompt v-else />
    </div>
  </div>
</template>

<script>
import { useStore } from "vuex";
import { defineComponent, computed } from "vue";

import Chat from "./Chat.vue";
import UsernamePrompt from "./UsernamePrompt.vue";

export default defineComponent({
  name: "AppMain",
  components: {
    Chat,
    UsernamePrompt,
  },
  setup() {
    const store = useStore();
    const username = computed(() => {
      if (store.state.username === "null") return null;

      return store.state.username;
    });

    function logout() {
      store.commit("UPDATE_USERNAME", null);
    }

    return {
      logout,
      username,
    };
  },
});
</script>

<style></style>
