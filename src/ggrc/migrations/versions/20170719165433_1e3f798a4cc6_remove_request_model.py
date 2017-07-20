# Copyright (C) 2017 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

"""Remove Request model."""
# disable Invalid constant name pylint warning for mandatory Alembic variables.
# pylint: disable=invalid-name

from alembic import op

from ggrc.migrations.utils.cleanup import replace
from ggrc.migrations.utils.cleanup import delete


# revision identifiers, used by Alembic.
revision = '1e3f798a4cc6'
down_revision = '47d3cb39bad7'


def upgrade():
  """Upgrade database schema and/or data, creating a new revision."""
  op.execute("DROP TABLE `requests`")

  replace(op, "audits", "object_type",
          old_value="Request", new_value="Assessment")

  deletions_required = (
      ("audit_objects", "auditable_type"),
      ("custom_attribute_definitions", "definition_type"),
      ("fulltext_record_properties", "type"),
      ("notifications", "object_type"),
      ("object_documents", "documentable_type"),
      ("object_owners", "ownable_type"),
      ("object_people", "personable_type"),
      ("relationships", "source_type"),
      ("relationships", "destination_type"),
      ("revisions", "resource_type"),
      ("revisions", "source_type"),
      ("revisions", "destination_type"),
  )

  for table, field in deletions_required:
    delete(op, table, field, value="Request")


def downgrade():
  """Downgrade database schema and/or data back to the previous revision."""
  # recreate Request table (query generated with SHOW CREATE TABLE)
  op.execute("""
      CREATE TABLE `requests` (
        `id` int(11) NOT NULL AUTO_INCREMENT,
        `request_type` enum('documentation','interview','population sample')
            NOT NULL,
        `status` enum('Not Started','In Progress','Ready for Review',
                      'Verified','Completed') NOT NULL,
        `start_date` date NOT NULL,
        `end_date` date NOT NULL,
        `audit_id` int(11) NOT NULL,
        `gdrive_upload_path` varchar(250) DEFAULT NULL,
        `created_at` datetime NOT NULL,
        `modified_by_id` int(11) DEFAULT NULL,
        `updated_at` datetime NOT NULL,
        `context_id` int(11) DEFAULT NULL,
        `test` text,
        `notes` text,
        `description` text,
        `requestor_id` int(11) DEFAULT NULL,
        `slug` varchar(250) NOT NULL,
        `title` varchar(250) NOT NULL,
        `audit_object_id` int(11) DEFAULT NULL,
        `finished_date` datetime DEFAULT NULL,
        `verified_date` datetime DEFAULT NULL,
        `recipients` varchar(250) DEFAULT NULL,
        `send_by_default` tinyint(1) DEFAULT NULL,
        PRIMARY KEY (`id`),
        UNIQUE KEY `uq_requests` (`slug`),
        KEY `audit_id` (`audit_id`),
        KEY `fk_requests_contexts` (`context_id`),
        KEY `ix_requests_updated_at` (`updated_at`),
        KEY `requests_audit_objects_ibfk` (`audit_object_id`),
        CONSTRAINT `requests_audit_objects_ibfk` FOREIGN KEY
            (`audit_object_id`) REFERENCES `audit_objects` (`id`),
        CONSTRAINT `requests_ibfk_2` FOREIGN KEY (`audit_id`) REFERENCES
            `audits` (`id`),
        CONSTRAINT `requests_ibfk_3` FOREIGN KEY (`context_id`) REFERENCES
            `contexts` (`id`)
      )
  """)

  # no way to restore removed values and nullified fields
