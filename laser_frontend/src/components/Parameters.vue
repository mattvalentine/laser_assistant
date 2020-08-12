<template>
  <div class="params">
    <p>
      Thickness (mm):
      <br />
      <input name="thickness" v-model="newThickness" type="number" step="0.1" @change="applyParams" />
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
      <input name="kerf" v-model="newKerf" type="number" step="0.01" @change="applyParams" />
    </p>
    <button @click="downloadsvg">Download</button>
  </div>
</template>

<script>
// const axios = require("axios").default;

export default {
  name: "Parameters",
  props: ["thickness", "kerf"],
  data: function () {
    return {
      newThickness: 3.1,
      newKerf: 0.27,
      material: "Acrylic",
    };
  },
  mounted() {
    this.newThickness = this.thickness;
    this.newKerf = this.kerf;
  },
  methods: {
    applyParams: function () {
      const floatThickness = parseFloat(this.newThickness);
      const floatKerf = parseFloat(this.newKerf);
      this.$emit("update", {
        thickness: floatThickness,
        kerf: floatKerf,
      });
      return;
    },
    downloadsvg: function () {
      this.$emit("download");
    },
  },
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