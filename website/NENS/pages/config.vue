<template>
 
  <v-container class="devices">
    <v-layout row wrap class="card">
      <v-flex v-for="(item, deviceId) in configure" :key="item.Name">
       <v-card class="card">
        {{deviceId}}
       <v-card-text >
        <div class="info">{{ item.Name }}</div>
        <div class="card">{{ item.Alias }}</div>
        <div class="info">{{ item.IPAddress }}</div>
       </v-card-text>
        </v-card>
      </v-flex>
    </v-layout>
  </v-container>


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
.card {
  padding: 0.1rem;
  background-color: #B9B9B7;
  border: 1px solid red;
  color: red;
  font-size: 1.35rem;
  text-align: center !important;
  margin: auto;
  margin-top: 0.5rem;
  margin-bottom: 0.5rem;
  margin-left: 0.5rem;
  margin-right: 0.5rem;
  flex: auto;
}
.info{
  font-size: 1.5rem;
  color: black;
}

</style>