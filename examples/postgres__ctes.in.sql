-- Common Table Expression (CTE) to gather all viewable item IDs based on write and read permissions
WITH viewable_items AS (
  -- Select item IDs with write permissions for the specified team and user
  SELECT item_id
  FROM item_write_permissions
  WHERE team_id = 'team_12345'
    AND (user_id IS NULL OR user_id = 'user_67890')
  
  UNION
  
  -- Select item IDs with read permissions for the specified team and user
  SELECT item_id
  FROM item_read_permissions
  WHERE team_id = 'team_12345'
    AND (user_id IS NULL OR user_id = 'user_67890')
),

-- CTE to extract component IDs from the items that are viewable and meet specific criteria
item_components AS (
  SELECT
    items.id AS item_id,
    -- Extract the component ID from the JSONB 'components' field and cast it to UUID
    (component.value->>'componentId')::uuid AS component_id
  FROM items
  -- Join with viewable_items to ensure only accessible items are processed
  JOIN viewable_items ON items.id = viewable_items.item_id
  -- Expand the JSONB 'components' field into key-value pairs
  CROSS JOIN LATERAL jsonb_each(items.details->'components') AS component(key, value)
  WHERE NOT items.is_archived -- Exclude archived items
    AND component.value->>'type' = 'component' -- Filter components by type
    AND component.value->>'componentType' IN ('typeA', 'typeB', 'typeC') -- Include specific component types
),

-- CTE to gather all viewable component IDs based on write and read permissions
viewable_components AS (
  -- Select component IDs with write permissions for the specified team and user
  SELECT component_id
  FROM component_write_permissions
  WHERE team_id = 'team_12345'
    AND (user_id IS NULL OR user_id = 'user_67890')
  
  UNION
  
  -- Select component IDs with read permissions for the specified team and user
  SELECT component_id
  FROM component_read_permissions
  WHERE team_id = 'team_12345'
    AND (user_id IS NULL OR user_id = 'user_67890')
),

-- CTE to combine component IDs from item_components and viewable_components
all_components AS (
  SELECT component_id FROM item_components
  UNION
  SELECT component_id FROM viewable_components
)

-- Final SELECT statement to retrieve detailed information about accessible components
SELECT
  components.id AS id,
  components.name,
  components.updated_at
FROM components
-- Join with all_components to ensure only accessible components are selected
JOIN all_components ON components.id = all_components.component_id
WHERE
  components.status = 'active' -- Filter for active components
  AND components.category = 'analytics' -- Filter by specific category
ORDER BY
  components.updated_at DESC -- Order the results by the most recently updated
LIMIT 50
OFFSET 10;
