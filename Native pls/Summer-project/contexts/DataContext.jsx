import { createContext, useState } from "react";

export const DataContext = createContext();

export const DataProvider = ({ children }) => {
  const [loading, setLoading] = useState(false);
  const [userName, setUserName] = useState("Salai");

  return (
    <DataContext.Provider
      value={{ loading, setLoading, userName, setUserName}}
    >
      {children}
    </DataContext.Provider>
  );
};