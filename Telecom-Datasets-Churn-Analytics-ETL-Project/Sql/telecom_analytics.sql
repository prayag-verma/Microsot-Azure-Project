SET ANSI_NULLS ON;
GO
SET QUOTED_IDENTIFIER ON;
GO
CREATE TABLE [dbo].[telecom_analytics](
	[CustomerID] [varchar](50) NOT NULL,
	[Gender] [varchar](10) NULL,
	[SeniorCitizen] [bit] NULL,
	[Partner] [varchar](5) NULL,
	[Dependents] [varchar](5) NULL,
	[Tenure] [int] NULL,
	[PhoneService] [varchar](5) NULL,
	[MultipleLines] [varchar](20) NULL,
	[InternetService] [varchar](20) NULL,
	[OnlineSecurity] [varchar](20) NULL,
	[OnlineBackup] [varchar](20) NULL,
	[DeviceProtection] [varchar](20) NULL,
	[TechSupport] [varchar](20) NULL,
	[StreamingTV] [varchar](20) NULL,
	[StreamingMovies] [varchar](20) NULL,
	[Contract] [varchar](20) NULL,
	[PaperlessBilling] [varchar](5) NULL,
	[PaymentMethod] [varchar](30) NULL,
	[MonthlyCharges] [decimal](10, 2) NULL,
	[TotalCharges] [decimal](10, 2) NULL,
	[Churn] [varchar](5) NULL,
	[LoadDate] [datetime] NULL
) ON [PRIMARY];
GO
ALTER TABLE [dbo].[telecom_analytics] ADD CONSTRAINT [PK_telecom_analytics] PRIMARY KEY CLUSTERED ([CustomerID] ASC);
GO
CREATE NONCLUSTERED INDEX [IX_telecom_analytics_churn] ON [dbo].[telecom_analytics]([Churn] ASC);
GO
ALTER TABLE [dbo].[telecom_analytics] ADD DEFAULT (getdate()) FOR [LoadDate];
GO