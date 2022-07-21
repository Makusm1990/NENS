<template>
  <v-card>
    <v-card-title>
      <v-text-field
        v-model="search"
        placeholder="Datum Format YYYY-MM-DD"
        append-icon="mdi-magnify"
        label="Search"
        single-line
        hide-details
      ></v-text-field>
    </v-card-title>
    <v-data-table
      :headers="headers"
      :items="alarmData"
      :search="search"
      class="table">

      <template v-slot:item.date="{item}">
        {{formatTimestamp(item)}}
      </template>

      <template v-slot:item.id="{item}">
        <nuxt-link :to="'/Notfall_ID/' + item.id">
          {{item.id}}
        </nuxt-link>
      </template>

    </v-data-table>
  </v-card>
</template>

<script>
  export default {
    data () {
      return {
        search: '',
        alarmData: [],
        headers: [
          { text: 'Eintrag', value: 'id'},
          { text: 'Ausgelöst von Gerät', value: 'device' },
          { text: 'IPv4', value: 'ipv4' },
          { text: 'Datum', value: 'date' },
        ],
      };
    },
    async fetch() {
      await this.loadData();
      },

  methods: {
      async loadData() {
      const dataAll = await fetch("http://localhost:8080").then((res) => res.json())
      this.alarmData = dataAll
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