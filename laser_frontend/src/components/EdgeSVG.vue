<template>
  <div class="edge-model" v-html="edge_svg"></div>
</template>

<script>
const axios = require("axios").default;

// const edgeClicked = () => {
//   console.log("blah");
//   return;
// };

export default {
  name: "EdgeSVG",
  data() {
    return {
      edge_svg: "",
    };
  },
  mounted() {
    axios
      .get("http://localhost:5000/get_edges")
      .then((response) => (this.edge_svg = response.data));
  },
};
</script>

<style>
.edge-model {
  grid-column: 1 / 4;
  grid-row: 1;
  display: grid;
  align-items: center;
  z-index: 10;
}

.edges:hover {
  opacity: 1;
}
.edges {
  opacity: 0;
  stroke: #ec008c;
  stroke-width: 3px;
}
</style>
