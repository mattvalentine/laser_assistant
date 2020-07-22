<template>
  <div id="app" class="ui">
    <OutputSVG v-if="svgLoaded" :outsvg="outputModel" />
    <EdgeSVG v-if="svgLoaded" v-on:addJoint="addJoint" :edge_data="inputModel.edge_data" />
    <Parameters
      v-if="svgLoaded"
      v-on:update="updateParams"
      :thickness="laserParams.thickness"
      :kerf="laserParams.kerf"
    />
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
    LoadSVG,
  },
  data: function () {
    return {
      svgLoaded: false,
      outputModel: "<svg/>",
      inputModel: {},
      laserParams: {
        thickness: 3.1,
        kerf: 0.27,
      },
      AB: true,
      joint_index: 1,
    };
  },
  methods: {
    loadSVG: function (svgInput) {
      this.svgLoaded = true;
      let formData = new FormData();
      formData.append("svgInput", svgInput);
      // formData.append("laserParams", JSON.stringify(this.laserParams));

      axios
        .post("get_model", formData, {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        })
        .then((response) => {
          this.inputModel = response.data;
          this.updateOutput();
        });
    },
    updateOutput: function () {
      let formData = new FormData();
      formData.append("inputModel", JSON.stringify(this.inputModel));
      formData.append("laserParams", JSON.stringify(this.laserParams));
      // this.outputModel = outsvg;
      axios
        .post("get_output", formData, {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        })
        .then((response) => {
          this.outputModel = response.data;
        });
    },
    updateParams: function (newParams) {
      console.log(newParams);
      this.laserParams = newParams;
      this.updateOutput();
    },
    addJoint: function (edge) {
      const jointName =
        "J" + this.joint_index.toString() + (this.AB ? "A" : "B");
      this.inputModel.joints[jointName] = { path: edge.d, face: edge.face };

      this.AB = !this.AB;
      if (this.AB === true) {
        this.joint_index += 1;
      }

      this.updateOutput();
    },
  },
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

.model {
  grid-column: 1 / 4;
  grid-row: 1;
  display: grid;
  align-items: center;
  /* z-index: 0; */
  width: 100%;
}
</style>
