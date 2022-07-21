<template>
    <div>
        <div class="header-cards card-deck">
            <div class="row">
                <div class="card">
                    <div class="card-body h2">
                        <h2 class="card-title">Fallnummer</h2>
                            {{Notfall_ID}}
                    </div>

                </div>
                <div class="card ">
                    <div class="card-body h2">
                        <h2 class="card-title">Meldender PC</h2>
                            {{Notfall_Device}}
                    </div>
                </div>
                <div class="card ">
                    <div class="card-body h2">
                        <h2 class="card-title">IP Adresse</h2>
                            {{Notfall_IP}}
                    </div>
                </div>
                <div class="card ">
                    <div class="card-body h2">
                        <h2 class="card-title">Datum</h2>
                            {{formatTimestamp(Notfall_Datum)}}
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
    export default {
        components: {
            },
        data () {
            return {
                Notfall_ID: null,
                Notfall_Device: null,
                Notfall_IP: null,
                Notfall_Datum: null,
            };
        },
    async fetch() {
        await this.loadData();
    },

    methods: {
        async loadData() {
            const dataAll = await fetch("http://localhost:8080/Notfall_ID/"+this.$route.params.Notfall_ID).then((res) => res.json())
            this.Notfall_ID = dataAll.id
            this.Notfall_Device = dataAll.device
            this.Notfall_IP = dataAll.ipv4
            this.Notfall_Datum = dataAll.date
            //console.log(this.Notfall_ID)
        },

        formatTimestamp(Notfall_Datum) {
            return new Date(Notfall_Datum).toLocaleString()
        },
    }
    }
</script>

<style>
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
.card-deck {
    flex: 1 0 0%;
    margin-right: 15px;
    margin-bottom: 0;
    margin-left: 15px;
    display: flex;
    margin: auto;
}

.card-title {
    color :black
}


</style>