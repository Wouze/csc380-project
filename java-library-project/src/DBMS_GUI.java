import javax.swing.*;
import java.awt.*;
import java.sql.*;

public class DBMS_GUI {

    private static Connection connect;

    /**
     * @wbp.parser.entryPoint
     */
    public static void main(String[] args) {
        SwingUtilities.invokeLater(() -> {
            initializeDatabase();

            JFrame mainFrame = new JFrame("Library Management System");
            mainFrame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
            mainFrame.setSize(1000, 700);

            JTabbedPane tabbedPane = new JTabbedPane();

            // Author Tab
            Author authorPanel = new Author();
            tabbedPane.addTab("Authors", authorPanel.getPanel(connect));

            // Book Tab
            BookWindow bookPanel = new BookWindow();
            tabbedPane.addTab("Books", bookPanel.getPanel(connect));

            // Member Tab
            MemberWindow memberPanel = new MemberWindow();
            tabbedPane.addTab("Members", memberPanel.getPanel(connect));

            // Library Card Tab
            libraryCard cardPanel = new libraryCard();
            tabbedPane.addTab("Library Cards", cardPanel.getPanel(connect));

            // Book-Author Tab
            BookAuthorWindow baPanel = new BookAuthorWindow();
            tabbedPane.addTab("Book-Author", baPanel.getPanel(connect));

            mainFrame.add(tabbedPane);
            mainFrame.setVisible(true);
        });
    }

    /**
     * @wbp.parser.entryPoint
     */
    private static void initializeDatabase() {
        String url = "jdbc:mysql://localhost:3306/csc380_project";
        String username = "root";
        String password = "Moe3319@";
        try {
            Class.forName("com.mysql.cj.jdbc.Driver");
            connect = DriverManager.getConnection(url, username, password);
            System.out.println("Database connected.");
        } catch (Exception e) {
            e.printStackTrace();
            JOptionPane.showMessageDialog(null, "Database connection failed.");
            System.exit(1);
        }
    }

    /**
     * @wbp.parser.entryPoint
     */
    public static Connection getConnection() {
        return connect;
    }
}
