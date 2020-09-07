export default function (h, row, index) {
  const changed = (rowId, newColor) => {
    console.log(rowId, newColor);
    console.log(this.toChange);
    this.toChange.push([rowId, newColor]);
  };
  return (
    <b-form-select
      id="basicSelect"
      plain={true}
      options={[
        "red",
        "blue",
        "pink",
        "gold",
        "black",
        "silver",
        "white",
        "navy blue",
        "ivory",
        "green",
        "orange",
        "brown",
        "gray",
        "beige",
        "yellow",
        "purple",
      ]}
      value={row.main_color}
      on-change={(e) => changed(row._id, e)}
    />
  );
}
