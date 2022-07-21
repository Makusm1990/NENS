<template>
  <v-card>
  <v-container class="devices">
    <v-layout row wrap class="card">
      <v-flex v-for="(item, deviceId) in configure" :key="item.Name" >
       <v-card flat class="card">
        {{deviceId}}
       <v-card-text>
        <div>{{ item.Name }}</div>
        <div>{{ item.Alias }}</div>
        <div>{{ item.IPAddress }}</div>
       </v-card-text>
        </v-card>
      </v-flex>
    </v-layout>
  </v-container>

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
.card {
  padding: 1rem;
  background-color: #B9B9B7;
  border: 1px solid red;
  color: red;
  font-size: 1.35rem;
  text-align: center !important;
  margin: auto;
  margin-top: 1rem;
  margin-bottom: 1rem;
  margin-left: 1rem;
  margin-right: 1rem;
  flex: auto;
}

</style>