<template>
  <v-app dark>
    <v-navigation-drawer
      v-model="drawer"
      :clipped="clipped"
      fixed
      app
    >
      <v-list>
        <v-list-item
          v-for="(item, i) in items"
          :key="i"
          :to="item.to"
          router
          exact
        >
          <v-list-item-action>
            <v-icon>{{ item.icon }}</v-icon>
          </v-list-item-action>
          <v-list-item-content>
            <v-list-item-title v-text="item.title" />
          </v-list-item-content>
        </v-list-item>
      </v-list>
    </v-navigation-drawer>
    <v-app-bar :clipped-left="clipped" fixed app>
      <v-app-bar-nav-icon @click.stop="drawer = !drawer" />
    </v-app-bar>
    <v-main>
      <v-container>
        <Nuxt />
      </v-container>
    </v-main>
    <v-footer :absolute="!fixed" app>
      <span>&copy; {{ new Date().getFullYear() }}</span>
    </v-footer>
  </v-app>
</template>

<script>
export default {
  name: 'DefaultLayout',
  data() {
    return {
      clipped: false,
      drawer: false,
      fixed: false,
      items: [
        {
          icon: 'mdi-apps',
          title: 'Startseite',
          to: '/',
        },
        {
          icon: 'mdi-cards-variant',
          title: 'Configure',
          to: '/config',
        },
      ],
    }
  },
}
</script>

<style>
table{
  width: 100%;
  border: 1px solid #ddd;
  padding: 1px;
}
td{
  border: 1px solid #ddd;
  padding: 8px;
  color: black;
}
tr{
  background-color: #b9b9b780;
  color: black;
}

tr:nth-child(even){background-color: #B9B9B7;}

tr:hover {background-color: #B9B9B7;}

th {
  padding-top: 12px;
  padding-bottom: 12px;
  text-align: left;
  background-color: #af0c0c;
  color: black;
  padding-left: 8px;
}

span {
  color: black
}

a {
  color: black;
  text-decoration: underline  red;
  text-decoration-style: double;
}
.v-application a {
    color: black;
}

.theme--dark.v-btn.v-btn--has-bg {
    background-color: transparent;
    width: 100%;
    color: black;
}
.v-data-table > .v-data-table__wrapper > table > tbody > tr > th, .v-data-table > .v-data-table__wrapper > table > thead > tr > th, .v-data-table > .v-data-table__wrapper > table > tfoot > tr > th {
    -webkit-user-select: none;
    -moz-user-select: none;
    user-select: none;
    font-size: 1.35rem;
    height: 48px;
}
.mdi-arrow-up::before {
    content: "\F005D";
}
.mdi:before {
    display: inline-block;
    font: normal normal normal 24px/1 "Material Design Icons";
    font-size: inherit;
    text-rendering: auto;
    line-height: inherit;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    color: black !important;
}
::before, ::after {
    text-decoration: inherit;
    vertical-align: inherit;
}
*, ::before, ::after {
    background-repeat: no-repeat;
    box-sizing: inherit;
}
</style>
