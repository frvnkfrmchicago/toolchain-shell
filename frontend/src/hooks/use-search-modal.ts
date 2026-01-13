"use client";

import { useState, useEffect, useCallback } from "react";

interface UseSearchModalReturn {
  isOpen: boolean;
  initialQuery: string;
  openModal: (query?: string) => void;
  closeModal: () => void;
}

export function useSearchModal(): UseSearchModalReturn {
  const [isOpen, setIsOpen] = useState(false);
  const [initialQuery, setInitialQuery] = useState("");

  const openModal = useCallback((query: string = "") => {
    setInitialQuery(query);
    setIsOpen(true);
  }, []);

  const closeModal = useCallback(() => {
    setIsOpen(false);
  }, []);

  // Command+K / Ctrl+K keyboard shortcut
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      // Open modal with Cmd+K or Ctrl+K
      if ((e.metaKey || e.ctrlKey) && e.key === "k") {
        e.preventDefault();
        openModal();
      }

      // Close modal with Escape
      if (e.key === "Escape" && isOpen) {
        e.preventDefault();
        closeModal();
      }
    };

    window.addEventListener("keydown", handleKeyDown);
    return () => window.removeEventListener("keydown", handleKeyDown);
  }, [isOpen, openModal, closeModal]);

  return {
    isOpen,
    initialQuery,
    openModal,
    closeModal,
  };
}
