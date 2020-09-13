<template>
  <div class="params">
    <p>
      Scale factor:
      <br />
      <input name="scale" v-model="newScaleFactor" type="number" step="0.1" @change="applyParams" />
    </p>
    <p>
      Thickness (mm):
      <br />
      <input name="thickness" v-model="newThickness" type="number" step="0.1" @change="applyParams" />
    </p>

    <p>
      Material
      <br />
      <select name="material" v-model="newMaterial" @change="applyParams">
        <option disabled value>Please select one</option>
        <option>Wood</option>
        <option>Acrylic</option>
        <!-- <option>C</option> -->
      </select>
    </p>

    <p>
      Kerf (mm):
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
  props: ["thickness", "kerf", "material", "scaleFactor"],
  data: function () {
    return {
      newThickness: 3.0,
      newKerf: 0.05,
      newMaterial: "Wood",
      newScaleFactor: 1.0,
    };
  },
  mounted() {
    this.newThickness = this.thickness;
    this.newKerf = this.kerf;
    this.newMaterial = this.material;
    this.newScaleFactor = this.scaleFactor;
  },
  methods: {
    applyParams: function () {
      const floatThickness = parseFloat(this.newThickness);
      const floatKerf = parseFloat(this.newKerf);
      const floatScaleFactor = parseFloat(this.newScaleFactor);
      this.$emit("update", {
        thickness: floatThickness,
        kerf: floatKerf,
        material: this.newMaterial,
        scaleFactor: floatScaleFactor,
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
  grid-area: panel;
  background-color: #d2d8de;
  margin: 10px;
  padding: 10px;
  border-radius: 10px;
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.6);
}
</style>