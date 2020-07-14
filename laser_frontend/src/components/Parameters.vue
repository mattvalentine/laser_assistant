<template>
  <div class="params">
    <p>
      Thickness (mm):
      <br />
      <input name="thickness" v-model="thickness" />
    </p>

    <p>
      Material
      <br />
      <select name="material" v-model="material">
        <option disabled value>Please select one</option>
        <option>Wood</option>
        <option>Acrylic</option>
        <!-- <option>C</option> -->
      </select>
    </p>

    <p>
      Kerf Radius (mm):
      <br />
      <input name="kerf" v-model="kerf" />
    </p>
    <button @click="applyParams">Apply</button>
  </div>
</template>

<script>
const axios = require("axios").default;

export default {
  name: "Parameters",
  data: function() {
    return {
      thickness: 3.1,
      kerf: 0.27,
      material: "Acrylic"
    };
  },
  methods: {
    applyParams: function() {
      axios
        .get("http://localhost:5000/parameters", {
          params: {
            kerf: this.kerf,
            material: this.material,
            thickness: this.thickness
          }
        })
        .then(response => this.$emit("outsvg", response.data));
      return;
    }
  }
};
</script>

<style scoped>
.params {
  grid-column: 4 / 5;
  grid-row: 1;
  background-color: lightgrey;
  margin: 1vmin;
  padding: 1vmin;
  border-radius: 2vmin;
}
</style>