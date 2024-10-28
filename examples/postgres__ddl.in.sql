-- ================================================
-- Table: items
-- Description: Stores information about items, including their details and archival status.
-- ================================================
CREATE TABLE items (
    id UUID PRIMARY KEY,                  -- Unique identifier for each item
    details JSONB NOT NULL,               -- JSONB column containing detailed information about the item, including components
    is_archived BOOLEAN DEFAULT FALSE     -- Indicates whether the item is archived
);

-- ================================================
-- Table: item_write_permissions
-- Description: Manages write permissions for items based on team and user.
-- ================================================
CREATE TABLE item_write_permissions (
    item_id UUID NOT NULL,                -- References the item that the permission applies to
    team_id VARCHAR(50) NOT NULL,         -- Identifier for the team
    user_id VARCHAR(50),                   -- Identifier for the user (NULL if the permission is public)
    PRIMARY KEY (item_id, team_id, user_id),
    FOREIGN KEY (item_id) REFERENCES items(id) ON DELETE CASCADE
);

-- ================================================
-- Table: item_read_permissions
-- Description: Manages read permissions for items based on team and user.
-- ================================================
CREATE TABLE item_read_permissions (
    item_id UUID NOT NULL,                -- References the item that the permission applies to
    team_id VARCHAR(50) NOT NULL,         -- Identifier for the team
    user_id VARCHAR(50),                   -- Identifier for the user (NULL if the permission is public)
    PRIMARY KEY (item_id, team_id, user_id),
    FOREIGN KEY (item_id) REFERENCES items(id) ON DELETE CASCADE
);

-- ================================================
-- Table: components
-- Description: Stores information about components, including their status and category.
-- ================================================
CREATE TABLE components (
    id UUID PRIMARY KEY,                  -- Unique identifier for each component
    name VARCHAR(255) NOT NULL,           -- Name of the component
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(), -- Timestamp of the last update
    status VARCHAR(50) NOT NULL,          -- Status of the component (e.g., 'active', 'inactive')
    category VARCHAR(50) NOT NULL         -- Category of the component (e.g., 'analytics', 'reporting')
);

-- ================================================
-- Table: component_write_permissions
-- Description: Manages write permissions for components based on team and user.
-- ================================================
CREATE TABLE component_write_permissions (
    component_id UUID NOT NULL,           -- References the component that the permission applies to
    team_id VARCHAR(50) NOT NULL,         -- Identifier for the team
    user_id VARCHAR(50),                   -- Identifier for the user (NULL if the permission is public)
    PRIMARY KEY (component_id, team_id, user_id),
    FOREIGN KEY (component_id) REFERENCES components(id) ON DELETE CASCADE
);

-- ================================================
-- Table: component_read_permissions
-- Description: Manages read permissions for components based on team and user.
-- ================================================
CREATE TABLE component_read_permissions (
    component_id UUID NOT NULL,           -- References the component that the permission applies to
    team_id VARCHAR(50) NOT NULL,         -- Identifier for the team
    user_id VARCHAR(50),                   -- Identifier for the user (NULL if the permission is public)
    PRIMARY KEY (component_id, team_id, user_id),
    FOREIGN KEY (component_id) REFERENCES components(id) ON DELETE CASCADE
);

-- ===================================================
-- Optional: Indexes to Optimize Query Performance
-- Description: Creating indexes on frequently queried columns to enhance performance.
-- ===================================================

-- Index on items.is_archived for faster filtering
CREATE INDEX idx_items_is_archived ON items(is_archived);

-- Index on components.status and components.category for faster filtering
CREATE INDEX idx_components_status_category ON components(status, category);

-- Indexes on permission tables to speed up permission checks
CREATE INDEX idx_item_write_permissions_team_user ON item_write_permissions(team_id, user_id);
CREATE INDEX idx_item_read_permissions_team_user ON item_read_permissions(team_id, user_id);
CREATE INDEX idx_component_write_permissions_team_user ON component_write_permissions(team_id, user_id);
CREATE INDEX idx_component_read_permissions_team_user ON component_read_permissions(team_id, user_id);
