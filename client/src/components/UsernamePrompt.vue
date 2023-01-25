<template>
  <div>
    <div>
      <h1 class="text-3xl">What's your name?</h1>
    </div>
    <div class="mt-8">
      <input type="text" v-model="username" v-on:keyup.enter="submit" />
    </div>
    <div class="mt-8">
      <button
        class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"
        @click="submit"
      >
        SUBMIT
      </button>
    </div>
  </div>
</template>

<script>
import { defineComponent, ref } from "vue";
import { useStore } from "vuex";

export default defineComponent({
  name: "UsernamePrompt",
  setup() {
    const username = ref(null);
    const store = useStore();

    function submit() {
      store.commit("UPDATE_USERNAME", username.value);
    }

    return {
      submit,
      username,
    };
  },
});
</script>

<style></style>
