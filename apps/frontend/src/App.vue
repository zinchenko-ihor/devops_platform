<template>
  <div style="padding: 40px">
    <h1>DevOps Demo</h1>

    <button @click="load">Get message</button>

    <h2 v-if="msg">{{ msg }}</h2>
  </div>
</template>

<script>
export default {
  data() {
    return {
      msg: ""
    }
  },

  methods: {
    async load() {
      const res = await fetch("/api/hello/")
      const data = await res.json()
      this.msg = data.message
    }
  }
}
</script>
