<template>
  <div id="app" class="ui">
    <OutputSVG v-if="svgLoaded" :outsvg="svgContent" />
    <EdgeSVG v-if="svgLoaded" v-on:outsvg="updateOutput" />
    <Parameters v-if="svgLoaded" v-on:outsvg="updateOutput" />
    <LoadSVG v-if="!svgLoaded" v-on:insvg="loadSVG" />
  </div>
</template>

<script>
import OutputSVG from "./components/OutputSVG";
import EdgeSVG from "./components/EdgeSVG";
import Parameters from "./components/Parameters";
import LoadSVG from "./components/LoadSVG";
const axios = require("axios").default;

export default {
  name: "App",
  components: {
    OutputSVG,
    EdgeSVG,
    Parameters,
    LoadSVG
  },
  data: function() {
    return {
      svgLoaded: false,
      svgContent: "<svg/>"
    };
  },
  methods: {
    loadSVG: function(svgInput) {
      this.svgLoaded = true;
      console.log(svgInput);
      axios
        .post("http://localhost:5000/get_output")
        .then(response => (this.svgContent = response.data));
    },
    updateOutput: function(outsvg) {
      this.svgContent = outsvg;
    }
  }
};
</script>

<style>
body {
  margin: 0;
}

.ui {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  grid-template-rows: 1fr;
  grid-column-gap: 1vw;
  width: vmin;
}
</style>
