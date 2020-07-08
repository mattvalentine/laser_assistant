<template>
  <div id="app" class="ui">
    <OutputSVG />
    <EdgeSVG />
    <Parameters />
  </div>
</template>

<script>
import OutputSVG from "./components/OutputSVG";
import EdgeSVG from "./components/EdgeSVG";
import Parameters from "./components/Parameters";

export default {
  name: "App",
  components: {
    OutputSVG,
    EdgeSVG,
    Parameters
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
