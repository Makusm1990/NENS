<template>
  <div class="container">
    <table class="table">
      <thead class="card">
        <tr>
          <th>Geräte ID</th>
          <th>Host Name</th>
          <th>Alias</th>
          <th>IP Adresse</th>
          <th></th>
        </tr>
      </thead>
        <tbody >
          <tr v-for="(item, deviceId) in configure" :key="item.Name">
            <td>{{deviceId}}</td>
            <td>{{item.Name}}</td>
            <td>{{item.Alias}}</td>
            <td>{{item.IPAddress}}</td>
            <td><v-btn>bearbeiten</v-btn></td>
          </tr>
        </tbody>
    </table>
  </div>
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


</style>