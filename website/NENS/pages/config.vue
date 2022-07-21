<template>
  <v-card>

  <v-card v-for="item in configure" :key="item.Alias"> {{ item.Name }} -- {{ item.Alias }} -- {{ item.IPAddress }}</v-card>

  </v-card>
</template>

<script>
  export default {
    data () {
      return {
        search: '',
        configure: [],
      };
    },
    async fetch() {
      await this.loadData();
      },

  methods: {
      async loadData() {
      const dataAll = await fetch("http://localhost:8080/config").then((res) => res.json())
      this.configure = dataAll
      },

      formatTimestamp(item) {
      return new Date(item.date).toLocaleString()
    },
    }
  }
</script>

<style>
table{
  color: whitesmoke;
}


</style>