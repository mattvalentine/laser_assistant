<template>
  <div class="loader">
    <span>
      <input class="loadbutton" type="file" id="SVGfile" @change="printFile" />
    </span>
  </div>
</template>

<script>
export default {
  name: "LoadSVG",
  methods: {
    printFile: async function(event) {
      const svgfile = event.target.files[0];
      const svgcontent = await new Response(svgfile).text();
      console.log(svgcontent);
      this.$emit("insvg", svgcontent);
      return;
    }
  }
};
</script>

<style>
.loader {
  grid-column: 1 / 5;
  grid-row: 1;
  display: grid;
  align-items: center;
  z-index: 10;
  height: 100vh;
  text-align: center;
}

.loadbutton {
  padding: 5vh;
  font-size: 4rem;
}
</style>