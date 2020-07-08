<template>
  <div class="output" v-html="output_svg"></div>
</template>

<script>
const axios = require("axios").default;

export default {
  name: "OutputSVG",
  data() {
    return {
      output_svg: "",
    };
  },
  mounted() {
    axios
      .get("http://localhost:5000/get_output")
      .then((response) => (this.output_svg = response.data));
  },
};
</script>

<style>
.output {
  grid-column: 1 / 4;
  grid-row: 1;
  display: grid;
  align-items: center;
  z-index: 0;
}
</style>
