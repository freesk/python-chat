<template>
  <div>
    <div class="flex-col flex" style="max-height: 500px; overflow-y: auto">
      <p
        :style="
          message.bot
            ? 'align-self: center; text-align: center;'
            : message.author === username
            ? 'align-self: start; text-align: left;'
            : 'align-self: end;  text-align: right;'
        "
        v-for="message in sorted"
        :key="message.id"
        class="mt-2 p-2"
        :class="message.bot ? 'bg-yellow-200' : null"
      >
        <span class="text-gray-500 text-sm">{{ message.postedAt }}</span>
        <br />
        <span class="text-gray-700 text-base" v-if="message.bot">
          {{ message.payload }}
        </span>
        <span
          class="text-gray-700 text-base"
          v-else-if="message.author === username"
        >
          You: {{ message.payload }}
        </span>
        <span class="text-gray-700 text-base" v-else>
          {{ message.author }}: {{ message.payload }}
        </span>
      </p>
    </div>
    <div class="mt-8 flex items-center justify-center">
      <textarea
        v-on:keyup.enter="submit"
        v-model="message"
        rows="4"
        cols="50"
        class="mr-8"
      />
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
import { io } from "socket.io-client";
import { v4 as uuidv4 } from "uuid";
import moment from "moment";
import { defineComponent, ref, computed } from "vue";
import { useStore } from "vuex";

export default defineComponent({
  name: "AppMain",
  setup() {
    const store = useStore();
    const username = computed(() => store.state.username);
    const message = ref(null);
    const messages = ref([]);
    const sorted = computed(() =>
      [...messages.value]
        .sort((a, b) => b.timestamp - a.timestamp)
        .map((message) => ({
          ...message,
          postedAt: moment(message.timestamp).format("llll"),
        }))
    );

    const socket = io("127.0.0.1:4000");

    socket.on("connect", () => {
      socket.emit("join", {
        username: username.value,
      });
    });

    socket.on("join", (data) => {
      console.log("join data", data);
      messages.value = [...data, ...messages.value];
    });

    socket.on("message", (data) => {
      messages.value = [...messages.value, data];
    });

    socket.on("disconnect", () => {
      console.log(`disconnected`);
    });

    function submit() {
      socket.emit("message", {
        payload: message.value,
        id: uuidv4(),
        author: username.value,
      });
      message.value = null;
    }

    return {
      submit,
      message,
      sorted,
      username,
    };
  },
});
</script>

<style></style>
