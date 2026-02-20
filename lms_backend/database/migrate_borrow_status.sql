-- Migration: Fix borrow_status check constraint to allow PENDING and REJECTED
-- Run this if your borrows table has the old CHECK constraint.
-- Valid values: PENDING, ACTIVE, RETURNED, REJECTED

ALTER TABLE borrows DROP CONSTRAINT IF EXISTS borrows_borrow_status_check;
ALTER TABLE borrows ADD CONSTRAINT borrows_borrow_status_check
  CHECK (borrow_status IN ('PENDING', 'ACTIVE', 'RETURNED', 'REJECTED', 'OVERDUE'));

-- Migrate existing rows: ISSUED -> ACTIVE
UPDATE borrows SET borrow_status = 'ACTIVE' WHERE borrow_status = 'ISSUED';
