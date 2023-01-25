import { createApp } from 'vue'
import { createStore } from 'vuex'
import Cookies from "js-cookie";

import App from './App.vue'
import './assets/tailwind.css'


const store = createStore({
    state () {
        return {
            username: Cookies.get("username")
        }
    },
    mutations: {
        UPDATE_USERNAME(state, payload) {
            Cookies.set("username", payload, { expires: 1 })
            state.username = payload
        }
    }
})

const app = createApp(App)

app.use(store)
app.mount('#app')
