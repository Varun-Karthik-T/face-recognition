import BottomNavBar from "@/components/BottomBar";
import { useContext, useEffect } from "react";
import { DataContext } from "@/contexts/DataContext";

export default function Index() {
  const {fetchPeople, setLoading } = useContext(DataContext);

  useEffect(() => {
    setLoading(true);
    fetchPeople();
  }, []);

  return <BottomNavBar />;
}
