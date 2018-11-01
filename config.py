CONNECTION_STRING = 'postgresql+psycopg2://ABurgess:gabby_tabby_120@localhost/postgres'

SQL = """
with my_block_group as (
select "GEOID" as geoid, geom
from in_bg_2018
where st_within(st_transform(st_setsrid(st_makepoint({lon}, {lat}), 4326), 2163), st_transform(geom, 2163))
)
SELECT jsonb_build_object(
    'type',     'FeatureCollection',
    'features', jsonb_agg(features.feature)
)
FROM (
  SELECT jsonb_build_object(
    'type',       'Feature',
    'id',         index,
    'geometry',   ST_AsGeoJSON(geom)::jsonb,
    'properties', to_jsonb(inputs) - 'geom'
  ) AS feature
  FROM (SELECT cr.* FROM crime.impd_ucr_crimes_2007_2017 cr, my_block_group as bg
          WHERE lower(cr."CRIME") like '%%homicide%%'
          AND ST_WITHIN(st_transform(cr.geom, 2163), st_buffer(st_transform(bg.geom, 2163), 5000))) inputs) features;
"""